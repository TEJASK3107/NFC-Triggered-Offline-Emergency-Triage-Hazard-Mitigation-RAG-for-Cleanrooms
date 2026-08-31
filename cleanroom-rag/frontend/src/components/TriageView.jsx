import React from 'react';
import VerificationBadge from './VerificationBadge';

export default function TriageView({ triage }) {
    if (!triage) return null;

    return (
        <div style={{
            marginTop: '20px',
            border: '2px solid #da3633',
            padding: '16px',
            borderRadius: '8px',
            backgroundColor: '#161b22'
        }}>
            <h3 style={{ color: '#f85149', marginTop: 0 }}>
                {triage.substance} (CAS: {triage.cas}) - {triage.station}
            </h3>
            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', fontSize: '15px' }}>
                {triage.instructions}
            </pre>
            <hr style={{ borderColor: '#30363d' }} />
            <VerificationBadge isMock={triage.is_mock} source={triage.source} />
        </div>
    );
}