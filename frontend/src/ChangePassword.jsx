
import { useState } from "react";

function ChangePassword() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  function handleChangePassword(e) {
    e.preventDefault();

    if (newPassword.length < 8) {
      setMessage("Password must be at least 8 characters.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage("New passwords do not match.");
      return;
    }

    if (oldPassword === newPassword) {
      setMessage("New password must be different.");
      return;
    }

    setMessage("Form validated. Backend connection pending.");
  }

  return (
    <div>
      <h1>Change Password</h1>

      <p>Preview only — password changes are not saved yet.</p>

      <form onSubmit={handleChangePassword}>
        <div>
          <label>Current Password</label>
          <input
            type="password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label>New Password</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            minLength={8}
            required
          />
        </div>

        <div>
          <label>Confirm New Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Change Password</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default ChangePassword;
