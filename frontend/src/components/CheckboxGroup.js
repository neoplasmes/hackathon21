import * as React from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

export const CheckboxGroup = ({ items, onItemChange }) => {
    if (!(items instanceof Map)) {
        throw new Error('maaaaaap');
    }

  return (
    <div>
      {items.forEach((value, key) => {
        
      })}
    </div>
  );
}