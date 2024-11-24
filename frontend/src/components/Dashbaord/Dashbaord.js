import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

import './Dashboard.css'

const backendEndpoint = process.env.REACT_APP_BACKEND_ENDPOINT;

const Dashboard = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch(backendEndpoint + '/api/data')
            .then(response => response.json())
            .then(data => setData(data))
            .then(data => {
                console.log('Fetched data:', data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div className='content-wrapper'>
            <ResponsiveContainer width='70%' aspect={2.0/1.0}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="linear" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default Dashboard;
