
import { useState } from "react";
import Register from "./Register";
import Login from "./Login";
import Records from "./Records";
import ChangePassword from "./ChangePassword";

function App() {
  const [page, setPage] = useState("register");

  return (
    <div>
      <nav>
        <button onClick={() => setPage("register")}>
          Register
        </button>

        <button onClick={() => setPage("login")}>
          Login
        </button>

        <button onClick={() => setPage("records")}>
          Records
        </button>

        <button onClick={() => setPage("changePassword")}>
          Change Password
        </button>
      </nav>

      {page === "register" && <Register />}
      {page === "login" && <Login />}
      {page === "records" && <Records />}
      {page === "changePassword" && <ChangePassword />}
    </div>
  );
}

export default App;
