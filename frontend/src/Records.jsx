
import { useState } from "react";

function Records() {
  const [name, setName] = useState("");
  const [course, setCourse] = useState("");
  const [phone, setPhone] = useState("");
  const [records, setRecords] = useState([]);

  function handleSubmit(e) {
    e.preventDefault();

    const newRecord = {
      name: name,
      course: course,
      phone: phone
    };

    setRecords([...records, newRecord]);

    setName("");
    setCourse("");
    setPhone("");
  }

  return (
    <div>
      <h1>Student Records</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Course</label>
          <input
            type="text"
            value={course}
            onChange={(e) => setCourse(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Phone</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </div>

        <button type="submit">Add Record</button>
      </form>

      <h2>Records List</h2>
      <p>Local preview only — not saved to database yet.</p>

      {records.length === 0 ? (
        <p>No records added yet.</p>
      ) : (
        <ul>
          {records.map((record, index) => (
            <li key={index}>
              {record.name} - {record.course} - {record.phone}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Records;
