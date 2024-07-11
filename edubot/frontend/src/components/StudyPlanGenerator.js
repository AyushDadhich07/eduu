import React, { useState } from 'react';
import axios from 'axios';

function StudyPlanGenerator() {
  const [durationDays, setDurationDays] = useState(7);
  const [studyPlan, setStudyPlan] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/generate-study-plan/', { duration_days: durationDays });
      setStudyPlan(response.data.study_plan);
    } catch (error) {
      console.error('Error generating study plan:', error);
    }
  };

  return (
    <div className="mb-4">
      <h2 className="text-2xl font-bold mb-2">Generate Study Plan</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={durationDays}
          onChange={(e) => setDurationDays(e.target.value)}
          className="w-full p-2 mb-2 border rounded"
          min="1"
          max="30"
        />
        <button type="submit" className="bg-purple-500 text-white px-4 py-2 rounded">
          Generate Study Plan
        </button>
      </form>
      {studyPlan && (
        <div className="mt-4">
          <h3 className="text-xl font-bold">Generated Study Plan:</h3>
          {Object.entries(studyPlan).map(([day, activities]) => (
            <div key={day} className="mt-2">
              <h4 className="text-lg font-semibold">{day}</h4>
              {activities.map((activity, index) => (
                <div key={index} className="ml-4">
                  {activity.topic && (
                    <>
                      <p><strong>{activity.topic}</strong></p>
                      <p>{activity.content}</p>
                    </>
                  )}
                  {activity.review && (
                    <p>Review topics: {activity.review.join(', ')}</p>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default StudyPlanGenerator;