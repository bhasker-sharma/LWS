import React, { useState, useEffect, useRef } from "react";
import { TiThMenuOutline } from 'react-icons/ti';
import {
  LineChart,
  XAxis,
  YAxis,
  Tooltip,
  Line,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";


function Graph() {

  const [data, setData] = useState([]);
  const bufferRef = useRef([]);
  const requestRef = useRef();

  const [showX, setShowX] = useState(true);
  const [showY, setShowY] = useState(true);
  const [showZ, setShowZ] = useState(true);
  const [yRange, setYRange] = useState(2000);

  const MaxPoints = 200;
  
  const processBuffer = () => {
    if (bufferRef.current.length > 0) {
      setData(prevData => {
        const newData = [
          ...prevData,
          ...bufferRef.current.splice(0, bufferRef.current.length)
        ];
  
        if (newData.length > MaxPoints) {
          return newData.slice(newData.length - MaxPoints);
        }
        return newData;
      });
    }
  
    requestRef.current = requestAnimationFrame(processBuffer);
  };
 useEffect(() => {
    const socket = new WebSocket("ws://192.168.1.177:8000/ws/graph");
  
    socket.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
  
        if (Array.isArray(parsedData)) {
          bufferRef.current.push(...parsedData.map(item => ({
            SNO: item.SNO,
            Xdata: parseFloat(item.Xdata),
            Ydata: parseFloat(item.Ydata),
            Zdata: parseFloat(item.Zdata),
          })));
        }
      } catch (error) {
        console.error("Error parsing WebSocket data:", error);
      }
    };
  
    // Start processing buffer
    requestRef.current = requestAnimationFrame(processBuffer);
  
    return () => {
      socket.close();
      cancelAnimationFrame(requestRef.current);
    };
  }, []);
  
  useEffect(() => {
    // console.log("Current data:", data);
  }, [data]);

  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMenuToggle = () => {
    setIsMenuOpen(!isMenuOpen);
  };

return (
    <>
  
    <div className="flex flex-col lg:flex-row flex-wrap">
    
      <div className="w-full lg:w-1/3 p-4">
        <div className="mb-4">
          <div className="flex flex-wrap items-center mb-2">
            <input
              name="Xdata"
              type="checkbox"
              checked={showX}
              onChange={(e) => setShowX(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="Xdata" className="mr-4">Xdata</label>
            <input
              name="Ydata"
              type="checkbox"
              checked={showY}
              onChange={(e) => setShowY(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="Ydata" className="mr-4">Ydata</label>
            <input
              name="Zdata"
              type="checkbox"
              checked={showZ}
              onChange={(e) => setShowZ(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="Zdata">Zdata</label>
          </div>
        </div>
  
        <div className="mb-4">
          <label htmlFor="yRange" className="block mb-2">Y-Axis Range Value:</label>
          <input
            type="number"
            id="yRange"
            value={yRange}
            onChange={(e) => setYRange(Number(e.target.value))}
            className="w-full sm:w-3/4 lg:w-1/2 p-2 border border-gray-300 rounded"
          />
        </div>
      </div>
 
    
      <div className="absolut top-0 right-0 w-[40%] lg:w-2/4  p-4">
        <div className="relative">
          <ResponsiveContainer
            className="w-full" 
            height={400}
          >
            <LineChart data={data} dataKey="value" margin={{ top: 5, right: 20, left: 10 }}>
              <XAxis dataKey="SNO" />
              <YAxis type="number" domain={[-yRange, yRange]} allowDataOverflow />
              <Tooltip />
              <Legend />
              <CartesianGrid stroke="#ccc" strokeOpacity={0.1} fill="#ffffff" />
              {showX && <Line type="monotone" dataKey="Xdata" strokeWidth={1} stroke="#000000" dot={true} />}
              {showY && <Line type="monotone" dataKey="Ydata" strokeWidth={1} stroke="#000000" />}
              {showZ && <Line type="monotone" dataKey="Zdata" strokeWidth={1} stroke="#000000" />}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  </>

  );
}

export default Graph;
