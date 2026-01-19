import { Outlet } from "react-router-dom";
import { Button } from "antd";
import { useNavigate } from "react-router";
function App() {
  const navigate = useNavigate();

  return (
    <>
      <Button onClick={() => navigate("/runs")}>goto Runs</Button>
      <Button onClick={() => navigate("/pending")}>goto Pending</Button>
      <Button onClick={() => navigate("/billing")}>goto billing</Button>
      <hr />
      <Outlet />
    </>
  );
}

export default App;
