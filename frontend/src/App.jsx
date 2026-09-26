import { BrowserRouter, Route, Routes } from "react-router-dom";

import Home from "./pages/Home";
import Interview from "./pages/Interview";
import NotFound from "./pages/NotFound";
import Result from "./pages/Result";
import ResumeUpload from "./pages/ResumeUpload";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/resume" element={<ResumeUpload />} />
        <Route path="/interview/:id" element={<Interview />} />
        <Route path="/result/:id" element={<Result />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;