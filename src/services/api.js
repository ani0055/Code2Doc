import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication APIs
export const register = async (email, name, password) => {
  try {
    const response = await api.post('/auth/register', {
      email,
      name,
      password,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Registration failed');
  }
};

export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

// Code Analysis API
export const analyzeCode = async (code, filename = 'file.py', includeDiagram = false) => {
  try {
    const response = await api.post('/analyze/code', {
      code,
      filename,
      include_diagram: includeDiagram,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Code analysis failed');
  }
};

// History APIs
export const getProjects = async () => {
  try {
    const response = await api.get('/history/projects');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch projects');
  }
};

export const getProjectDetails = async (projectId) => {
  try {
    const response = await api.get(`/history/projects/${projectId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch project details');
  }
};

export const getRecentProjects = async () => {
  try {
    const response = await api.get('/history/recent');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch recent projects');
  }
};

export const deleteProject = async (projectId) => {
  try {
    const response = await api.delete(`/history/projects/${projectId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete project');
  }
};
export const updateProjectName = async (projectId, newName) => {
  try {
    const response = await api.patch(`/history/projects/${projectId}`, {
      name: newName,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to update project name');
  }
};

// Export APIs
export const exportToPDF = async (markdown, filename = 'documentation', diagramImage = null) => {
  try {
    const response = await api.post('/export/pdf', {
      markdown,
      filename,
      diagram_image: diagramImage // Send base64 image
    }, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${filename}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'PDF export failed');
  }
};

export const exportToDOCX = async (markdown, filename = 'documentation', diagramImage = null) => {
  try {
    const response = await api.post('/export/docx', {
      markdown,
      filename,
      diagram_image: diagramImage 
    }, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${filename}.docx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'DOCX export failed');
  }
};

export const exportDocumentationPDF = async (docId) => {
  try {
    const response = await api.get(`/export/documentation/${docId}/pdf`, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `documentation_${docId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'PDF export failed');
  }
};

export const exportDocumentationDOCX = async (docId) => {
  try {
    const response = await api.get(`/export/documentation/${docId}/docx`, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `documentation_${docId}.docx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'DOCX export failed');
  }
};


export default api;