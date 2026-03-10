import google.generativeai as genai
from typing import Dict, Optional, List, Union
from app.config import settings
import logging
import asyncio
import re


logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        """Initialize Gemini API"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use one of the available models from your list
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Fast and efficient
    
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
        """Create prompt for documentation generation with explicit formatting rules."""
        
        functions_count = len(structure.get('functions', []))
        classes_count = len(structure.get('classes', []))
        
        functions_list = "\n".join([f"- {func['name']}" for func in structure.get('functions', [])])
        classes_list = "\n".join([f"- {cls['name']}" for cls in structure.get('classes', [])])
        
        # --- CRITICAL FIX: EXPLICITLY DEFINE NESTED LIST FORMATTING ---
        prompt = f"""You are a technical documentation expert. Generate comprehensive, clear documentation for this {language} code.
        
**MANDATORY FORMATTING INSTRUCTION:** Use **nested markdown lists** for methods/attributes/parameters. Every item must be nested using 2 spaces for the first level of detail and 4 spaces for the second level of detail. Do NOT use flat lists for method details.

Example of correct formatting for a method:
```markdown
* ***method_name(args)***:
  * **Purpose:** What it does.
  * **Parameters:**
    * `param1 (type)`: Description of param1.
    * `param2 (type)`: Description of param2.
```
**End of Mandatory Formatting Instruction.**

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
For each function, use the nested list format specified above.
## Classes (if any)
For each class:
### Purpose: What the class represents
### Attributes: List class attributes using the nested list format.
### Methods: List and explain methods using the nested list format.
## Dependencies
List imported modules/libraries and their purpose.
## Usage Example
Provide a complete, working example of how to use this code.

Generate clear, professional documentation now:"""
        return prompt

    def _create_diagram_prompt(self, code: str, structure: Dict, language: str) -> str:
        """Create prompt for flow diagram generation"""
        
        functions_list = ', '.join([f['name'] for f in structure.get('functions', [])])
        classes_list = ', '.join([c['name'] for c in structure.get('classes', [])])
        
        prompt = f"""Generate a code flow diagram in a simple JSON format for this {language} code.

    Code Structure:
    - Functions: {functions_list or 'none'}
    - Classes: {classes_list or 'none'}

    Code:
    ```{language}
    {code[:800]}
    ```

    Create a flow diagram showing:
    1. Main entry point
    2. Function calls
    3. Class relationships
    4. Data flow

    Return ONLY a JSON object in this exact format (no other text):
    {{
    "nodes": [
        {{"id": "start", "label": "Start", "color": "#4CAF50"}},
        {{"id": "func1", "label": "function_name()", "color": "#2196F3"}},
        {{"id": "class1", "label": "ClassName", "color": "#FF9800"}}
    ],
    "edges": [
        {{"from": "start", "to": "func1", "label": "calls"}},
        {{"from": "func1", "to": "class1", "label": "uses"}}
    ]
    }}

    Rules:
    - Use "start" as the entry point
    - Each function should be a node with id like "func_functionname"
    - Each class should be a node with id like "class_classname"
    - Show the flow with edges (arrows)
    - Keep it simple and clear

    Generate the JSON now:"""
        
        return prompt