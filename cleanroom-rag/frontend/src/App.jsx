import React, { useState } from 'react';
import NFCScanner from './components/NFCScanner';
import TriageView from './components/TriageView';

export default function App() {
    const [status, setStatus] = useState('System Ready. Tap NFC Tag.');
    const [triage, setTriage] = useState(null);

    const handleScan = async (payload) => {
        setStatus('Transmitting payload over air-gapped Wi-Fi...');
        try {
            const res = await fetch('http://localhost:8000/api/triage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            setTriage(data);
            setStatus('SOP Action Plan Loaded.');
        } catch (err) {
            setStatus('Connection Error: Check Wi-Fi connection.');
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#0d1117', color: '#c9d1d9', minHeight: '100vh' }}>
            <h2 style={{ color: '#58a6ff' }}>Cleanroom Triage Interface</h2>
            <NFCScanner onScan={handleScan} setStatus={setStatus} />
            <p style={{ marginTop: '12px' }}><b>Status:</b> {status}</p>
            <TriageView triage={triage} />
        </div>
    );
}