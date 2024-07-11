import React, { useState } from 'react';
import axios from 'axios';

function QuestionGenerator() {
  const [numQuestions, setNumQuestions] = useState(5);
  const [questions, setQuestions] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/generate-questions/', { num_questions: numQuestions });
      setQuestions(response.data.qa_pairs);
    } catch (error) {
      console.error('Error generating questions:', error);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-bold mb-2">Generate Study Questions</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={numQuestions}
          onChange={(e) => setNumQuestions(e.target.value)}
          className="w-full p-2 mb-2 border rounded"
          min="1"
          max="20"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Generate Questions
        </button>
      </form>
      {questions.length > 0 && (
        <div className="mt-4">
          <h3 className="text-xl font-bold">Generated Questions:</h3>
          {questions.map((qa, index) => (
            <div key={index} className="mt-2">
              <p><strong>Q: {qa.question}</strong></p>
              <p>A: {qa.answer}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default QuestionGenerator;