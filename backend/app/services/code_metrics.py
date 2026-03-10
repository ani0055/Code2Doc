import logging
from typing import Dict, List
import subprocess
import tempfile
import os

logger = logging.getLogger(__name__)

class CodeMetricsService:
    
    def analyze_code_quality(self, code: str, language: str) -> Dict:
        """Analyze code quality metrics"""
        
        metrics = {
            'lines_of_code': 0,
            'complexity': {
                'average': 0,
                'max': 0,
                'functions': []
            },
            'maintainability_index': 0,
            'code_smells': [],
            'suggestions': []
        }
        
        if language == 'python':
            try:
                from radon.complexity import cc_visit
                from radon.metrics import mi_visit
                from radon.raw import analyze
                metrics.update(self._analyze_python(code))
            except Exception as e:
                logger.error(f"Python analysis failed: {e}")
                metrics.update(self._fallback_analysis(code, language))
        else:
            # Use fallback for all non-Python languages
            metrics.update(self._analyze_with_lizard(code, language))
        
        # Add suggestions based on metrics
        metrics['suggestions'] = self._generate_suggestions(metrics)
        
        return metrics
    
    def _analyze_python(self, code: str) -> Dict:
        """Analyze Python code with radon"""
        from radon.complexity import cc_visit
        from radon.metrics import mi_visit
        from radon.raw import analyze
        
        try:
            # Lines of code
            raw_analysis = analyze(code)
            loc = raw_analysis.loc
            sloc = raw_analysis.sloc
            comments = raw_analysis.comments
            
            # Cyclomatic complexity
            complexity_data = cc_visit(code)
            complexities = [item.complexity for item in complexity_data]
            avg_complexity = sum(complexities) / len(complexities) if complexities else 0
            max_complexity = max(complexities) if complexities else 0
            
            function_complexities = [
                {
                    'name': item.name,
                    'complexity': item.complexity,
                    'rank': self._get_complexity_rank(item.complexity)
                }
                for item in complexity_data
            ]
            
            # Maintainability Index
            mi_score = mi_visit(code, multi=True)
            avg_mi = sum(mi_score) / len(mi_score) if mi_score else 100
            
            # Code smells
            code_smells = []
            if max_complexity > 10:
                code_smells.append({
                    'type': 'High Complexity',
                    'severity': 'warning',
                    'message': f'Maximum complexity of {max_complexity} detected. Consider refactoring.'
                })
            
            if avg_mi < 20:
                code_smells.append({
                    'type': 'Low Maintainability',
                    'severity': 'warning',
                    'message': f'Maintainability index is {avg_mi:.1f}. Code may be hard to maintain.'
                })
            
            if comments == 0 and sloc > 20:
                code_smells.append({
                    'type': 'No Comments',
                    'severity': 'info',
                    'message': 'No comments found. Consider adding documentation.'
                })
            
            return {
                'lines_of_code': loc,
                'source_lines': sloc,
                'comment_lines': comments,
                'blank_lines': raw_analysis.blank,
                'complexity': {
                    'average': round(avg_complexity, 2),
                    'max': max_complexity,
                    'functions': function_complexities
                },
                'maintainability_index': round(avg_mi, 2),
                'code_smells': code_smells
            }
            
        except Exception as e:
            logger.error(f"Error in Python analysis: {e}")
            return self._fallback_analysis(code, 'python')
    
    def _analyze_with_lizard(self, code: str, language: str) -> Dict:
        """Analyze code using Lizard with better error handling"""
        try:
            # Map language to file extension
            ext_map = {
                'javascript': 'js',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c',
                'typescript': 'ts'
            }
            
            extension = ext_map.get(language, 'txt')
            
            # Write code to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{extension}', delete=False, encoding='utf-8') as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            
            try:
                # Run lizard as subprocess for better error handling
                result = subprocess.run(
                    ['lizard', tmp_path, '-l', language],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    logger.warning(f"Lizard failed with code {result.returncode}")
                    return self._fallback_analysis(code, language)
                
                # Parse lizard output
                return self._parse_lizard_output(result.stdout, code, language)
                
            except subprocess.TimeoutExpired:
                logger.error("Lizard analysis timed out")
                return self._fallback_analysis(code, language)
            except FileNotFoundError:
                logger.error("Lizard not found, using fallback")
                return self._fallback_analysis(code, language)
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error in lizard analysis: {e}")
            return self._fallback_analysis(code, language)
    
    def _parse_lizard_output(self, output: str, code: str, language: str) -> Dict:
        """Parse lizard command output"""
        lines = output.strip().split('\n')
        
        # Extract metrics from output
        nloc = 0
        avg_ccn = 0
        functions = []
        
        for line in lines:
            if 'NLOC' in line and 'CCN' in line:
                # Parse function line
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        ccn = int(parts[0])
                        nloc_val = int(parts[1])
                        func_name = parts[-1] if len(parts) > 2 else 'unknown'
                        
                        functions.append({
                            'name': func_name,
                            'complexity': ccn,
                            'rank': self._get_complexity_rank(ccn),
                            'lines': nloc_val
                        })
                    except (ValueError, IndexError):
                        continue
        
        if functions:
            complexities = [f['complexity'] for f in functions]
            avg_ccn = sum(complexities) / len(complexities)
            max_ccn = max(complexities)
            total_nloc = sum(f['lines'] for f in functions)
        else:
            # No functions found, use line count
            total_nloc = len([l for l in code.split('\n') if l.strip()])
            avg_ccn = 2
            max_ccn = 5
        
        mi = self._calculate_simple_mi(total_nloc, avg_ccn, len(functions))
        
        code_smells = []
        if max_ccn > 10:
            code_smells.append({
                'type': 'High Complexity',
                'severity': 'warning',
                'message': f'Maximum complexity of {max_ccn} detected.'
            })
        
        if total_nloc > 500:
            code_smells.append({
                'type': 'Large File',
                'severity': 'info',
                'message': 'File is quite large. Consider splitting into multiple files.'
            })
        
        return {
            'lines_of_code': total_nloc or len(code.split('\n')),
            'source_lines': total_nloc or len([l for l in code.split('\n') if l.strip()]),
            'complexity': {
                'average': round(avg_ccn, 2),
                'max': max_ccn,
                'functions': functions
            },
            'maintainability_index': mi,
            'code_smells': code_smells,
            'function_count': len(functions)
        }
    
    def _fallback_analysis(self, code: str, language: str) -> Dict:
        """Fallback analysis when tools fail"""
        lines = code.split('\n')
        source_lines = [l for l in lines if l.strip() and not l.strip().startswith('//') and not l.strip().startswith('#')]
        
        # Count functions/methods by looking for keywords
        func_keywords = {
            'python': ['def '],
            'java': ['public ', 'private ', 'protected '],
            'javascript': ['function ', 'const ', 'let ', '=>']
        }
        
        keywords = func_keywords.get(language, ['function'])
        func_count = sum(1 for line in source_lines if any(kw in line for kw in keywords))
        
        loc = len(source_lines)
        # Estimate complexity
        estimated_complexity = min(10, max(2, loc / 20))
        
        return {
            'lines_of_code': len(lines),
            'source_lines': loc,
            'comment_lines': len(lines) - loc,
            'complexity': {
                'average': round(estimated_complexity, 1),
                'max': round(estimated_complexity * 1.5, 1),
                'functions': []
            },
            'maintainability_index': max(50, min(100, 100 - (loc / 10))),
            'code_smells': [{
                'type': 'Analysis Limited',
                'severity': 'info',
                'message': 'Full complexity analysis unavailable. Estimates provided based on line count.'
            }],
            'function_count': func_count
        }
    
    def _get_complexity_rank(self, complexity: int) -> str:
        """Get complexity rank (A-F)"""
        if complexity <= 5:
            return 'A'
        elif complexity <= 10:
            return 'B'
        elif complexity <= 20:
            return 'C'
        elif complexity <= 30:
            return 'D'
        elif complexity <= 40:
            return 'E'
        else:
            return 'F'
    
    def _calculate_simple_mi(self, loc: int, complexity: float, num_functions: int) -> float:
        """Calculate a simplified maintainability index"""
        if loc == 0:
            return 100
        
        mi = 171 - 5.2 * complexity - 0.23 * loc
        mi = max(0, min(100, mi))
        return round(mi, 2)
    
    def _generate_suggestions(self, metrics: Dict) -> List[str]:
        """Generate improvement suggestions based on metrics"""
        suggestions = []
        
        complexity = metrics.get('complexity', {})
        avg_complexity = complexity.get('average', 0)
        max_complexity = complexity.get('max', 0)
        mi = metrics.get('maintainability_index', 0)
        
        if max_complexity > 15:
            suggestions.append('🔴 Very high complexity detected. Urgent refactoring recommended - break down complex functions.')
        elif max_complexity > 10:
            suggestions.append('🟡 High complexity detected. Consider breaking down complex functions into smaller ones.')
        
        if avg_complexity > 7:
            suggestions.append('🟡 Average complexity is elevated. Look for opportunities to simplify logic.')
        elif avg_complexity <= 5:
            suggestions.append('🟢 Good complexity levels! Code structure is clear.')
        
        if mi < 20:
            suggestions.append('🔴 Low maintainability score. Code may be difficult to maintain - consider major refactoring.')
        elif mi < 50:
            suggestions.append('🟡 Moderate maintainability. Add comments and refactor complex sections.')
        else:
            suggestions.append('🟢 Good maintainability score! Code is relatively easy to understand.')
        
        loc = metrics.get('lines_of_code', 0)
        if loc > 500:
            suggestions.append('📏 Large file detected. Consider splitting into multiple modules for better organization.')
        
        comment_lines = metrics.get('comment_lines', 0)
        if comment_lines == 0 and loc > 50:
            suggestions.append('📝 No comments found. Add documentation for better code understanding.')
        
        if not suggestions:
            suggestions.append('✅ Code quality looks good overall!')
        
        return suggestions