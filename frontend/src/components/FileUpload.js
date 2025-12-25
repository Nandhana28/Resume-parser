import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import axios from 'axios';

const FileUpload = ({ onUploadSuccess, loading, setLoading }) => {
  const handleDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    setLoading(true);
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const resp = await axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess(resp.data);
    } catch (err) {
      console.error('Upload error:', err);
      const errMsg = err.response?.data?.error || err.message || 'Unknown error';
      alert(`Error uploading file: ${errMsg}`);
      setLoading(false);
    }
  }, [onUploadSuccess, setLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    multiple: false
  });

  if (loading) {
    return (
      <motion.div
        className="uploadCard"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
      >
        <div className="loading">
          <div className="spinner"></div>
          <h3>Analyzing your resume</h3>
          <p>Scraping latest jobs and finding matches...</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="uploadCard"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    >
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        <h3>Drop your resume here</h3>
        <p>or click to browse (PDF, DOCX, DOC files)</p>
      </div>
    </motion.div>
  );
};

export default FileUpload;
