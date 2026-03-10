import google.generativeai as genai
from typing import Dict, Optional
from app.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        """Initialize Gemini API"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def _call_gemini(self, prompt: str) -> str:
        """
        Helper to safely call the synchronous Gemini API using asyncio.to_thread.
        """
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error in _call_gemini: {str(e)}")
            raise Exception(f"Failed to generate content: {str(e)}")

    async def generate_documentation(
        self, 
        code: str, 
        code_structure: Dict,
        language: str,
        include_diagram: bool = False
    ) -> Dict[str, str]:
        """Generate documentation using Gemini AI"""
        
        try:
            # Generate main documentation
            doc_prompt = self._create_documentation_prompt(code, code_structure, language)
            documentation = await self._call_gemini(doc_prompt)
            
            result = {
                'markdown': documentation,
                'diagram': None
            }
            
            # Generate diagram if requested
            if include_diagram:
                diagram_prompt = self._create_diagram_prompt(code, code_structure, language)
                diagram = await self._call_gemini(diagram_prompt)
                result['diagram'] = diagram
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return {
                'markdown': f"Error generating documentation: {str(e)}",
                'diagram': None
            }

    def _create_documentation_prompt(self, code: str, structure: Dict, language: str) -> str:
        """Create prompt for documentation generation"""
        
        functions_count = len(structure.get('functions', []))
        classes_count = len(structure.get('classes', []))
        
        functions_list = "\n".join([f"- {func['name']}" for func in structure.get('functions', [])])
        classes_list = "\n".join([f"- {cls['name']}" for cls in structure.get('classes', [])])
        
        prompt = f"""You are a technical documentation expert. Generate comprehensive, clear documentation for this {language} code.

Code Structure Summary:
- Language: {language}
- Functions: {functions_count}
{functions_list if functions_list else "  (none)"}
- Classes: {classes_count}
{classes_list if classes_list else "  (none)"}

Code to document:
```{language}
{code}
```

Generate professional documentation in markdown format with these sections:

## Overview
Brief description of what this code does (2-3 sentences).

## Functions
For each function, explain:
- **Purpose**: What it does
- **Parameters**: List each parameter with type and description
- **Returns**: What it returns
- **Example Usage**: Show how to use it

## Classes (if any)
For each class:
- **Purpose**: What the class represents
- **Attributes**: List class attributes
- **Methods**: List and explain methods

## Dependencies
List imported modules/libraries and their purpose.

## Usage Example
Provide a complete, working example of how to use this code.

Generate clear, professional documentation now:"""
        
        return prompt
    
    def _create_diagram_prompt(self, code: str, structure: Dict, language: str) -> str:
        """Constructs the prompt specifically for Mermaid diagram generation."""
        
        prompt = f"""Generate a Mermaid diagram for this {language} code structure.

Code Structure:
- Functions: {[f['name'] for f in structure.get('functions', [])]}
- Classes: {[c['name'] for c in structure.get('classes', [])]}

Code context (first 500 characters):
```{language}
{code[:500]}
```

Create a flowchart using Mermaid syntax that shows:
1. Main entry points
2. Function calls and relationships
3. Data flow

Return ONLY valid Mermaid syntax (start with 'graph TD' or 'flowchart TD').
Do not include markdown code fences, just the raw Mermaid syntax.

Example format:
graph TD
    A[Start] --> B[Function 1]
    B --> C[Function 2]
    C --> D[End]

Generate the Mermaid diagram now:"""
        
        return prompt