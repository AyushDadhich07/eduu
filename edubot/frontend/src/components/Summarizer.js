import React, { useState } from 'react';
import axios from 'axios';

function Summarizer() {
  const [keywords, setKeywords] = useState('');
  const [summary, setSummary] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/summarize/', { keywords });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error generating summary:', error);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-bold mb-2">Summarizer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          className="w-full p-2 mb-2 border rounded"
          placeholder="Enter keywords (optional)"
        />
        <button type="submit" className="bg-yellow-500 text-white px-4 py-2 rounded">
          Generate Summary
        </button>
      </form>
      {summary && (
        <div className="mt-4">
          <h3 className="text-xl font-bold">Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default Summarizer;