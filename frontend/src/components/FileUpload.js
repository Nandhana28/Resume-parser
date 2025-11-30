import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import axios from 'axios';

const FileUpload = ({ onUploadSuccess, loading, setLoading }) => {
  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    setLoading(true);
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess(response.data);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file. Please try again.');
      setLoading(false);
    }
  }, [onUploadSuccess, setLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    multiple: false
  });

  if (loading) {
    return (
      <motion.div
        className="upload-card"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
      >
        <div className="loading">
          <div className="spinner"></div>
          <h3>Analyzing your resume</h3>
          <p>Finding the best job matches for you</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="upload-card"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    >
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        <h3>Drop your resume here</h3>
        <p>or click to browse (.docx files)</p>
      </div>
    </motion.div>
  );
};

export default FileUpload;
