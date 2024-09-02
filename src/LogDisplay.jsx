import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './LogDisplay.css'

const LogDisplay = () => {
  const [logs, setLogs] = useState([])
  const [year, setYear] = useState('')
  const [month, setMonth] = useState('')
  const [day, setDay] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  useEffect(() => {
    fetchLogs()
  }, [year, month, day, page])

  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/get-logs/', {
        params: {
          year: year || null,
          month: month || null,
          day: day || null,
          page: page,
        },
      })

      if (response.data && response.data.logs) {
        setLogs(response.data.logs)
        setTotalPages(response.data.total_pages || 1)
      } else {
        setLogs([])
        setTotalPages(1)
      }
    } catch (error) {
      console.error('Error fetching logs:', error)
      setLogs([])
      setTotalPages(1)
    }
  }

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1)
    }
  }

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1)
    }
  }

  return (
    <div className="container">
      <h2 style={{ textAlign: 'center' }}>Tabla logs</h2>
      <div className="filter-container">
        <span style={{ marginRight: '10px' }}>Filter:</span>
        <input
          type="text"
          placeholder="Year"
          maxLength="2"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
        <input
          type="text"
          placeholder="Month"
          maxLength="2"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <input
          type="text"
          placeholder="Day"
          maxLength="2"
          value={day}
          onChange={(e) => setDay(e.target.value)}
        />
      </div>

      <div className="logs-table-container">
        <table className="logs-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Date</th>
              <th>Event</th>
              <th>Recipient</th>
              <th>URL</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan="6">No logs available</td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id}>
                  <td>{log.id}</td>
                  <td>{log.date}</td>
                  <td>{log.event}</td>
                  <td>{log.recipient}</td>
                  <td>
                    <a href={log.url} target="_blank" rel="noopener noreferrer">
                      {log.url}
                    </a>
                  </td>
                  <td className="log-message">{JSON.stringify(log.message)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="pagination-controls">
        <button
          className="pagination-button"
          onClick={handlePreviousPage}
          disabled={page === 1}
        >
          Previous
        </button>
        <span className="pagination-info">
          Page {page} of {totalPages}
        </span>
        <button
          className="pagination-button"
          onClick={handleNextPage}
          disabled={page === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default LogDisplay;
