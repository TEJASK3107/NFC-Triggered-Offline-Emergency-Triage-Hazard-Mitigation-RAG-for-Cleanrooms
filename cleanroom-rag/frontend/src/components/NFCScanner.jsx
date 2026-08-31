import React from 'react';

export default function NFCScanner({ onScan, setStatus }) {
    const triggerScan = async () => {
        if ('NDEFReader' in window) {
            try {
                const ndef = new NDEFReader();
                await ndef.scan();
                setStatus('Scanning... Tap device against station NFC tag.');

                ndef.onreading = async (event) => {
                    const decoder = new TextDecoder();
                    for (const record of event.message.records) {
                        const text = decoder.decode(record.data);
                        onScan(JSON.parse(text));
                    }
                };
            } catch (err) {
                setStatus('NFC Hardware Error: ' + err.message);
            }
        } else {
            // Offline fallback mock trigger
            onScan({ station_id: "STATION-B4", substance: "Hydrazine", cas: "302-01-2" });
        }
    };

    return (
        <button
            onClick={triggerScan}
            style={{
                padding: '16px',
                width: '100%',
                fontSize: '18px',
                fontWeight: 'bold',
                backgroundColor: '#da3633',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer'
            }}>
            SCAN STATION NFC TAG
        </button>
    );
}