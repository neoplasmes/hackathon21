import * as React from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Divider, FormGroup, Box } from '@mui/material';
import { abbreviationsToRussian } from '../model/constants';
import { TOGGLE_ONE, TOGGLE_GROUP } from '../model/reducer';

const checkboxPadding = "5px";

export const CheckboxGroup = ({ items, stateDispatch, filtersState, groupID }) => {
    if (!(items instanceof Map)) {
        throw new Error('maaaaaap');
    }
    
    const allSelected = Object.values(filtersState[groupID]).every(Boolean);
    const someSelected = Object.values(filtersState[groupID]).some(Boolean);

    const handleItemChange = (event) => {
        stateDispatch({
          type: TOGGLE_ONE,
          group: groupID,
          item: event.target.value
        })
    };

    const handleGroupChange = (event) => {
        stateDispatch({
          type: TOGGLE_GROUP,
          group: groupID,
          allIs: someSelected ? false : true,
        })
    };

    return (
        <FormGroup sx={{ width: '20%' }}>
            <FormControlLabel 
                label={abbreviationsToRussian[groupID]}
                slotProps={{ typography: { fontSize: '1rem', fontWeight: 'bold' } }}
                control={
                    <Checkbox
                        indeterminate={someSelected && !allSelected}
                        size="medium"
                        value={groupID}
                        checked={allSelected}
                        onChange={handleGroupChange}
                        sx={{ padding: checkboxPadding }}
                    />
                }
            />
            <Box sx={{ display: 'flex', flexDirection: 'column', ml: 2 }}>
                {[...items].map(([key, value]) => {
                    console.log(value, key)

                    return (
                        <FormControlLabel
                            key={key}
                            slotProps={{ typography: { fontSize: "0.75rem" } }}
                            label={value}
                            control={
                                <Checkbox
                                    size="small"
                                    value={key}
                                    checked={filtersState[groupID][key]}
                                    onChange={handleItemChange}
                                    sx={{ padding: checkboxPadding }}
                                />
                            }
                        />
                    );
                })}
            </Box>
            <Divider flexItem sx={{ color: "black" }}/>
        </FormGroup>
    );
}