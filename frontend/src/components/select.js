import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function MySelect({ label, options, value, onChange }) {
    const renderValue = value => {
        console.log("renderValue:", value);
        const selectedOption = options.find(option => option.value === value);
        console.log("selectedOption:", selectedOption); 
        return selectedOption ? selectedOption.label : "Не выбрано";
      };
return (
    <FormControl fullWidth>
    <InputLabel id={`${label}-label`}>{label}</InputLabel>
    <Select
        labelId={`${label}-label`}
        id={label}
        value={value}
        label={label}
        onChange={onChange}
        renderValue={renderValue}
    >
        {options.map((option) => (
        <MenuItem key={option.value} value={option.value}>
            {option.label}
        </MenuItem>
        ))}
    </Select>
    </FormControl>
);
}

export default MySelect;
