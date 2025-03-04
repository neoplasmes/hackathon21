import React, { useReducer, useState } from "react";
import { CheckboxGroup } from './components/CheckboxGroup'
import { mockData } from "./mockData";
import "./App.css";

const allKey = 'all';

const newMockData = mockData.map((el) => {
  const { campus, selected_role, education_level, question_category } = el;

  return {
    campus,
    selected_role,
    education_level,
    question_category,
  };
});

const educationLevels = [
  { value: "", label: "Не выбрано" },
  { value: "Бакалавриат", label: "бакалавриат" },
  { value: "Магистратура", label: "магистратура" },
  { value: "Специалитет", label: "специалитет" },
  { value: "Аспирантура", label: "аспирантура" },
];

const _educationLevels = new Map({
  all: 'Все',
  bak: 'Бакалавриат',
  mag: 'Магистратура',
  spec: 'Специалитет',
  asp: 'Аспирантура'
})

const questionCategories = [
  { value: "", label: "Не выбрано" },
  { value: "Деньги", label: "Деньги" },
  { value: "Учебный процесс", label: "Учебный процесс" },
  { value: "Практическая подготовка", label: "Практическая подготовка" },
  { value: "ГИА", label: "ГИА" },
  { value: "Траектории обучения", label: "Траектории обучения" },
  { value: "Английский язык", label: "Английский язык" },
  { value: "Цифровые компетенции", label: "Цифровые компетенции" },
  {
    value: "Перемещения студентов / Изменения статусов студентов",
    label: "Перемещения студентов / Изменения статусов студентов",
  },
  { value: "Онлайн-обучение", label: "Онлайн-обучение" },
  { value: "Цифровые системы", label: "Цифровые системы" },
  { value: "Обратная связь", label: "Обратная связь" },
  { value: "Дополнительное образование", label: "Дополнительное образование" },
  { value: "Безопасность", label: "Безопасность" },
  { value: "Наука", label: "Наука" },
  { value: "Социальные вопросы", label: "Социальные вопросы" },
  { value: "ВУЦ", label: "ВУЦ" },
  { value: "Общежития", label: "Общежития" },
  { value: "ОВЗ", label: "ОВЗ" },
  { value: "Внеучебка", label: "Внеучебка" },
  { value: "Выпускникам", label: "Выпускникам" },
  { value: "Другое", label: "Другое" },
];

const abbreviations = {
  campuses: 'camp',
  educactionLevels: 'edulvl',
  questionCategories: 'qstn',
};

const _campuses = new Map({
  all: "Все",
  msc: "Москва",
  nn: "Нижний Новгород",
  spb: "Санкт-Петербург",
  prm: "Пермь"
});

const createInitialFiltersState = (searchParams) => {
  const initialState = {};

  // group items must be map
  const constructFilterGroup = (groupAbbreviation, groupItems) => {
    initialState[groupAbbreviation] = {};

    const initialFilterItems = new Set(searchParams.get(groupAbbreviation).split(';'));

    for (const filterItem of groupItems.keys()) {
      initialState[groupAbbreviation][filterItem] = initialFilterItems.has(filterItem);
    }
  }

  constructFilterGroup(abbreviations.campuses, _campuses);
  constructFilterGroup(abbreviations.educactionLevels, _educationLevels)
}

const TOGGLE_ONE = 'TOGGLE_ONE';
const TOGGLE_GROUP = 'TOGGLE_GROUP';

const filtersReducer = (state, action) => {
  switch (action.type) {
    case TOGGLE_ONE:
      const newState = { ...state };
      newState[action.group][action.item] = !newState[action.group][action.item];
  }
}

function App() {
  const searchParams = new URLSearchParams(window.location.search);
  
  const [filtersState, dispatchFiltersChange] = useReducer(filtersReducer, new URLSearchParams(window.location.search), createInitialFiltersState);

  const handleCampusChange = (event) => {
    setSelectedCampus(event.target.value);
  };

  const handleEducationLevelChange = (event) => {
    setSelectedEducationLevel(event.target.value);
  };

  const handleQuestionCategoryChange = (event) => {
    setSelectedQuestionCategory(event.target.value);
  };

  const getLabelByValue = (value, options) => {
    const selectedOption = options.find((option) => option.value === value);
    return selectedOption ? selectedOption.label : "";
  };

  return (
      <div className="App">
        
      </div>
    );
}

export default App;
