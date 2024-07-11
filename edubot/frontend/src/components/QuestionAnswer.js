import React, { useState } from 'react';
import axios from 'axios';

function QuestionAnswer() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/question-answer/', { question });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Error getting answer:', error);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-bold mb-2">Ask a Question</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full p-2 mb-2 border rounded"
          placeholder="Enter your question"
        />
        <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
          Get Answer
        </button>
      </form>
      {answer && (
        <div className="mt-4">
          <h3 className="text-xl font-bold">Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default QuestionAnswer;