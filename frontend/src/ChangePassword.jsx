
import { useState } from "react";

export default function ChangePassword() {
  const [form, setForm] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setError("");

    if (form.new_password.length < 8) {
      setError("New password must be at least 8 characters.");
      return;
    }

    if (form.new_password !== form.confirm_password) {
      setError("New passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "/api/v1/auth/change-password",
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            old_password: form.old_password,
            new_password: form.new_password,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.error || `HTTP ${response.status}`
        );
      }

      setMessage(
        "Password changed successfully! Please log in again."
      );

      setForm({
        old_password: "",
        new_password: "",
        confirm_password: "",
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Change Password</h2>

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}

      {message && (
        <p style={{ color: "green" }}>{message}</p>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="password"
            name="old_password"
            placeholder="Current Password"
            value={form.old_password}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <input
            type="password"
            name="new_password"
            placeholder="New Password"
            value={form.new_password}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <input
            type="password"
            name="confirm_password"
            placeholder="Confirm New Password"
            value={form.confirm_password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Changing..." : "Change Password"}
        </button>
      </form>
    </div>
  );
}
