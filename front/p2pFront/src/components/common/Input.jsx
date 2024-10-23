import React from 'react';

export default function Input({ label, id, type, register, error }) {
  return (
    <div className="mb-3">
      <label htmlFor={id} className="form-label">{label}</label>
      <input {...register} type={type} className="form-control" id={id} />
      {error && <p className="text-danger">{error}</p>}
    </div>
  );
}
