import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';
import FileUpload from './components/FileUpload';
import Results from './components/Results';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUploadSuccess = (data) => {
    setResults(data);
    setLoading(false);
  };

  const handleReset = () => {
    setResults(null);
  };

  return (
    <div className="App">
      <motion.div 
        className="container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <header className="header">
          <motion.h1
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            AI Resume Parser
          </motion.h1>
          <p className="subtitle">Upload your resume and discover perfect job matches</p>
        </header>

        <AnimatePresence mode="wait">
          {!results ? (
            <FileUpload 
              key="upload"
              onUploadSuccess={handleUploadSuccess}
              loading={loading}
              setLoading={setLoading}
            />
          ) : (
            <Results 
              key="results"
              data={results}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}

export default App;
