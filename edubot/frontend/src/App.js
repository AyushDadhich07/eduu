import React, { useState } from 'react';
import PDFUploader from './components/PDFUploader';
import QuestionAnswer from './components/QuestionAnswer';
import Summarizer from './components/Summarizer';
import QuestionGenerator from './components/QuestionGenerator';
import QuestionPaperGenerator from './components/QuestionPaperGenerator';
import StudyPlanGenerator from './components/StudyPlanGenerator';

function App() {
  const [pdfProcessed, setPdfProcessed] = useState(false);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">PDF Learning Assistant</h1>
      <PDFUploader onProcessed={() => setPdfProcessed(true)} />
      {pdfProcessed && (
        <>
          <QuestionAnswer />
          <Summarizer />
          <QuestionGenerator />
          <QuestionPaperGenerator />
          <StudyPlanGenerator />
        </>
      )}
    </div>
  );
}

export default App;