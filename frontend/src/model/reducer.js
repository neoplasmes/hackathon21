import { campuses, educationLevels, questionCategories, abbreviations } from "./constants";

// action types
export const TOGGLE_ONE = 'TOGGLE_ONE';
export const TOGGLE_GROUP = 'TOGGLE_GROUP';
  
export const filtersReducer = (state, action) => {
    const newState = { ...state }
  
    switch (action.type) {
        case TOGGLE_ONE:
            newState[action.group][action.item] = !newState[action.group][action.item];

            return newState;
        case TOGGLE_GROUP:
            newState[action.group] = { ...state[action.group] };

            if (action.allIs === true) {
                for (const key in newState[action.group]) {
                newState[action.group][key] = true;
                }
            } else {
                for (const key in newState[action.group]) {
                newState[action.group][key] = false;
                }
            }

            return newState;
    }
}

export const createInitialFiltersState = (searchParams) => {
    const initialState = {};
  
    // group items must be map
    const constructFilterGroup = (groupAbbreviation, groupItems) => {
      initialState[groupAbbreviation] = {};
  
      const initialFilterItems = new Set(searchParams.get(groupAbbreviation)?.split(';'));
  
      for (const filterItem of groupItems.keys()) {
        initialState[groupAbbreviation][filterItem] = initialFilterItems.has(filterItem);
      }
    }
  
    constructFilterGroup(abbreviations.campuses, campuses);
    constructFilterGroup(abbreviations.educactionLevels, educationLevels);
    constructFilterGroup(abbreviations.questionCategories, questionCategories);
  
    return initialState;
}