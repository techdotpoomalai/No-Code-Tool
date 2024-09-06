import React, { useEffect, useState } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import './css/MenuStyle.css';

import Button from 'react-bootstrap/Button';


import Server from './Server/Server';
import axios from 'axios';

export default function Menu() {
  const [file, setFile] = useState(null);
  const [table_data, setTableData] = useState([]);
  const [table_load, setTableLoad] = useState(false)

  const server =new Server();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  }; 

  const handleSubmit = async (event) => {
  event.preventDefault();
    
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res=await server.file_upload(formData);
      console.log(res.data);
      setTableLoad(true);
    } catch (error) {
      console.error("Error uploading file:", error.res ? error.res.data : error.message);
    }
    
  };

  useEffect(() => {
    if (table_load){
      const res = axios.get('http://127.0.0.1:8000/fetch_data',{
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(res.data);
    }
  },[table_load]);

    return (
      <>
        <div class="row">
          <div class="col-2 menu">
          <h3>Load Data</h3>
          <div className='d-block'>
              <form onSubmit={handleSubmit}>
              <input type="file" onChange={handleFileChange} className='d-block'/><br/>
              <button type="submit" className='d-block'>Load Data</button>
              </form>
            </div><br/>

            <h3>Columns</h3>
            <div>
              {/* {headers.length > 0 ? (
                headers.map((val, k) => (
                  <label key={k} className='d-block'>
                    <input type="checkbox" name={val} />
                    {val}
                  </label>
                ))
              ) : (
                <p>No data</p>
              )} */}
            </div>
          </div>

          <div class="col-2 menu">

          </div>


          <div class="col-8 view">
            {/* <table>
              {response.length === 0 ? (
                <tbody>
                  <tr>
                    <td colSpan={headers.length}>Response Empty</td>
                  </tr>
                </tbody>
              ) : (
                <>
                  <thead>
                    <tr>
                      {headers.map((item, index) => (
                        <th key={index}>{item}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {response.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {headers.map((header, colIndex) => (
                          <td key={colIndex}>{row[header]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </>
              )}
            </table> */}
          </div>
          
        </div>
      </>
    );
  
}
