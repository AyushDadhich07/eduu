import React, { useState } from 'react';
import axios from 'axios';

function QuestionPaperGenerator() {
  const [numQuestions, setNumQuestions] = useState(20);
  const [questionPaper, setQuestionPaper] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/generate-question-paper/', { num_questions: numQuestions });
      setQuestionPaper(response.data.question_paper);
    } catch (error) {
      console.error('Error generating question paper:', error);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-bold mb-2">Generate Question Paper</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={numQuestions}
          onChange={(e) => setNumQuestions(e.target.value)}
          className="w-full p-2 mb-2 border rounded"
          min="10"
          max="50"
        />
        <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
          Generate Question Paper
        </button>
      </form>
      {questionPaper && (
        <div className="mt-4">
          <h3 className="text-xl font-bold">Generated Question Paper:</h3>
          {questionPaper.map((question, index) => (
            <div key={index} className="mt-2">
              <p><strong>{index + 1}. {question.question}</strong></p>
              {question.type === "MCQ" && (
                <ul className="list-disc list-inside">
                  {question.options.map((option, optIndex) => (
                    <li key={optIndex}>{option}</li>
                  ))}
                </ul>
              )}
              <p><em>Answer: {question.answer || question.correct_answer}</em></p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default QuestionPaperGenerator;