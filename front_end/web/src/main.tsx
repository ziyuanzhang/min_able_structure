import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App.jsx";
import Runs from "./pages/review/Runs.tsx";
import RunDetail from "./pages/review/RunDetail.tsx";
import Pending from "./pages/review/Pending.tsx";
import Billing from "./pages/Billing.tsx";
import Workflow from "./pages/workflow.tsx";

createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route path="runs" element={<Runs />}></Route>
        <Route path="runDetail/:requestId" element={<RunDetail />}></Route>
        <Route path="pending" element={<Pending />}></Route>
        <Route path="billing" element={<Billing />}></Route>
        <Route path="workflow/:requestId" element={<Workflow />}></Route>
      </Route>
    </Routes>
  </BrowserRouter>
);
