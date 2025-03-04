import React, { useReducer, useState } from "react";
import { CheckboxGroup } from './components/CheckboxGroup'
import { filtersReducer, createInitialFiltersState } from "./model/reducer";
import "./App.css";

const _educationLevels = new Map(Object.entries({
  bak: 'Бакалавриат',
  mag: 'Магистратура',
  spec: 'Специалитет',
  asp: 'Аспирантура'
}));

const _campuses = new Map(Object.entries({
  msc: "Москва",
  nn: "Нижний Новгород",
  spb: "Санкт-Петербург",
  prm: "Пермь"
}));

const _questionCategories = new Map(Object.entries({
  money: "Деньги",
  study: "Учебный процесс",
  pract: "Практическая подготовка",
  gia: "ГИА",
  traj: "Траектории обучения",
  eng: "Английский язык",
  digi: "Цифровые компетенции",
  move: "Перемещения студентов / Изменения статусов студентов",
  online: "Онлайн-обучение",
  sys: "Цифровые системы",
  feed: "Обратная связь",
  extra: "Дополнительное образование",
  sec: "Безопасность",
  sci: "Наука",
  soc: "Социальные вопросы",
  vuc: "ВУЦ",
  dorm: "Общежития",
  ovz: "ОВЗ",
  life: "Внеучебка",
  grad: "Выпускникам",
  other: "Другое",
}));

const abbreviations = {
  campuses: 'camp',
  educactionLevels: 'edulvl',
  questionCategories: 'qstn',
};




function App() {
  const [filtersState, dispatchFiltersChange] = useReducer(filtersReducer, new URLSearchParams(window.location.search), createInitialFiltersState);

  return (
      <div className="App">
        <CheckboxGroup 
          items={_campuses}
          filtersState={filtersState}
          groupID={abbreviations.campuses}
          stateDispatch={dispatchFiltersChange}
        />
        <CheckboxGroup 
          items={_educationLevels}
          filtersState={filtersState}
          groupID={abbreviations.educactionLevels}
          stateDispatch={dispatchFiltersChange}
        />
        <CheckboxGroup 
          items={_questionCategories}
          filtersState={filtersState}
          groupID={abbreviations.questionCategories}
          stateDispatch={dispatchFiltersChange}
        />
      </div>
    );
}

export default App;
