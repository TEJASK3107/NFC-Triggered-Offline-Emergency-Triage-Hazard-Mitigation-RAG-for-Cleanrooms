import React from 'react';

export default function VerificationBadge({ isMock, source }) {
    return (
        <div style={{ marginTop: '12px', display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{
                padding: '4px 8px',
                borderRadius: '4px',
                fontSize: '12px',
                fontWeight: 'bold',
                backgroundColor: isMock ? '#9e6a03' : '#238636',
                color: '#ffffff'
            }}>
                {isMock ? 'SYSTEM: MOCK MODE' : 'SYSTEM: LANCE-DB VERIFIED'}
            </span>
            <span style={{ fontSize: '12px', color: '#8b949e' }}>Ref: {source}</span>
        </div>
    );
}