from tree_sitter import Parser, Language
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_java as tsjava

class CodeParser:
    def __init__(self):
        """Initialize parsers for different languages"""
        # Create parsers with languages directly
        self.parsers = {
            'python': self._create_parser(Language(tspython.language())),
            'javascript': self._create_parser(Language(tsjavascript.language())),
            'java': self._create_parser(Language(tsjava.language()))
        }
    
    def _create_parser(self, language):
        """Create a parser for a specific language"""
        parser = Parser()
        parser.language = language  # Use .language property instead of set_language()
        return parser
    
    def detect_language(self, filename: str) -> str:
        """Detect programming language from file extension"""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.tsx': 'javascript',
            '.java': 'java'
        }
        for ext, lang in extensions.items():
            if filename.endswith(ext):
                return lang
        return 'python'  # default
    
    def parse_code(self, code: str, language: str) -> dict:
        """Parse code and extract structure"""
        parser = self.parsers.get(language)
        if not parser:
            raise ValueError(f"Language {language} not supported")
        
        tree = parser.parse(bytes(code, "utf8"))
        structure = self._extract_structure(tree.root_node, code, language)
        return structure
    
    def _extract_structure(self, node, code: str, language: str) -> dict:
        """Extract functions, classes, imports from AST"""
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'language': language
        }
        
        def get_node_text(node):
            return code[node.start_byte:node.end_byte]
        
        def traverse(node):
            # Python specific
            if language == 'python':
                if node.type == 'function_definition':
                    func_name_node = node.child_by_field_name('name')
                    params_node = node.child_by_field_name('parameters')
                    if func_name_node:
                        structure['functions'].append({
                            'name': get_node_text(func_name_node),
                            'params': get_node_text(params_node) if params_node else '()',
                            'code': get_node_text(node)[:200] + '...'
                        })
                
                elif node.type == 'class_definition':
                    class_name_node = node.child_by_field_name('name')
                    if class_name_node:
                        structure['classes'].append({
                            'name': get_node_text(class_name_node),
                            'code': get_node_text(node)[:200] + '...'
                        })
                
                elif node.type in ['import_statement', 'import_from_statement']:
                    structure['imports'].append(get_node_text(node))
            
            # JavaScript/TypeScript specific
            elif language == 'javascript':
                if node.type in ['function_declaration', 'arrow_function', 'function']:
                    name_node = node.child_by_field_name('name')
                    name = get_node_text(name_node) if name_node else 'anonymous'
                    structure['functions'].append({
                        'name': name,
                        'code': get_node_text(node)[:200] + '...'
                    })
                
                elif node.type == 'class_declaration':
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        structure['classes'].append({
                            'name': get_node_text(name_node),
                            'code': get_node_text(node)[:200] + '...'
                        })
            
            # Java specific
            elif language == 'java':
                if node.type == 'method_declaration':
                    name_node = node.child_by_field_name('name')
                    params_node = node.child_by_field_name('parameters')
                    if name_node:
                        structure['functions'].append({
                            'name': get_node_text(name_node),
                            'params': get_node_text(params_node) if params_node else '()',
                            'code': get_node_text(node)[:200] + '...'
                        })
                
                elif node.type == 'class_declaration':
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        structure['classes'].append({
                            'name': get_node_text(name_node),
                            'code': get_node_text(node)[:200] + '...'
                        })
                
                elif node.type == 'import_declaration':
                    structure['imports'].append(get_node_text(node))
            
            # Traverse children
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return structure