
import { useEffect, useState } from "react";

export default function Records() {
  const [records, setRecords] = useState([]);
  const [form, setForm] = useState({
    name: "",
    course: "",
    phone: "",
  });

  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
      ...options,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || `HTTP ${response.status}`);
    }

    return result;
  }

  async function loadRecords() {
    try {
      setError("");

      const result = await apiRequest("/api/v1/records");

      setRecords(result.data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadRecords();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const url =
        editingId === null
          ? "/api/v1/records"
          : `/api/v1/records/${editingId}`;

      const method = editingId === null ? "POST" : "PUT";

      await apiRequest(url, {
        method,
        body: JSON.stringify(form),
      });

      setMessage(
        editingId === null
          ? "Record created successfully!"
          : "Record updated successfully!"
      );

      setForm({
        name: "",
        course: "",
        phone: "",
      });

      setEditingId(null);

      await loadRecords();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(record) {
    setEditingId(record.id);

    setForm({
      name: record.name,
      course: record.course,
      phone: record.phone,
    });

    setMessage("");
    setError("");
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this record?")) {
      return;
    }

    setError("");
    setMessage("");
    setLoading(true);

    try {
      await apiRequest(`/api/v1/records/${id}`, {
        method: "DELETE",
      });

      setMessage("Record deleted successfully!");

      if (editingId === id) {
        setEditingId(null);
        setForm({ name: "", course: "", phone: "" });
      }

      await loadRecords();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Student Records</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {message && (
        <p style={{ color: "green" }}>{message}</p>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="text"
            name="name"
            placeholder="Student Name"
            value={form.name}
            onChange={handleChange}
            required
            maxLength={100}
          />
        </div>

        <div>
          <input
            type="text"
            name="course"
            placeholder="Course"
            value={form.course}
            onChange={handleChange}
            required
            maxLength={100}
          />
        </div>

        <div>
          <input
            type="tel"
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
            required
            maxLength={30}
          />
        </div>

        <button type="submit" disabled={loading}>
          {editingId === null
            ? "Create Record"
            : "Update Record"}
        </button>

        {editingId !== null && (
          <button
            type="button"
            onClick={() => {
              setEditingId(null);
              setForm({ name: "", course: "", phone: "" });
            }}
          >
            Cancel Edit
          </button>
        )}
      </form>

      <hr />

      <h3>My Records</h3>

      {records.length === 0 ? (
        <p>No records found.</p>
      ) : (
        <ul>
          {records.map((record) => (
            <li key={record.id}>
              <p>
                <strong>Name:</strong> {record.name}
              </p>

              <p>
                <strong>Course:</strong> {record.course}
              </p>

              <p>
                <strong>Phone:</strong> {record.phone}
              </p>

              <button
                type="button"
                disabled={loading}
                onClick={() => handleEdit(record)}
              >
                Edit
              </button>

              <button
                type="button"
                disabled={loading}
                onClick={() => handleDelete(record.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
