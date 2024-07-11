import React, { useState } from 'react';
import axios from 'axios';

function PDFUploader({ onProcessed }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/process-pdf/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onProcessed();
    } catch (error) {
      console.error('Error processing PDF:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input type="file" onChange={handleFileChange} accept=".pdf" className="mb-2" />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Upload and Process PDF
      </button>
    </form>
  );
}

export default PDFUploader;