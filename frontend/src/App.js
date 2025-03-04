import React, { useState } from 'react';
import MySelect from './components/select';
import { mockData } from './mockData';
import './App.css';

const newMockData = mockData.map(el => {
  const { campus, selected_role, education_level, question_category } = el;

  return {
    campus,
    selected_role,
    education_level,
    question_category
  }
})

const campuses = [
  {value:'', label: 'Не выбрано'},
  { value: 'Москва', label: 'Москва' },
  { value: 'Нижний Новгород', label: 'Нижний Новгород' },
  { value: 'Санкт-Петербург', label: 'Санкт-Петербург' },
  { value: 'Пермь', label: 'Пермь' },
];

const educationLevels = [
  {value:'', label: 'Не выбрано'},
  { value: 'Бакалавриат', label: 'бакалавриат' },
  { value: 'Магистратура', label: 'магистратура' },
  { value: 'Специалитет', label: 'специалитет' },
  { value: 'Аспирантура', label: 'аспирантура' },
];

const questionCategories = [
  {value:'', label: 'Не выбрано'},
  { value: 'Деньги', label: 'Деньги' },
  { value: 'Учебный процесс', label: 'Учебный процесс' },
  { value: 'Практическая подготовка', label: 'Практическая подготовка' },
  { value: 'ГИА', label: 'ГИА' },
  { value: 'Траектории обучения', label: 'Траектории обучения' },
  { value: 'Английский язык', label: 'Английский язык' },
  { value: 'Цифровые компетенции', label: 'Цифровые компетенции' },
  { value: 'Перемещения студентов / Изменения статусов студентов', label: 'Перемещения студентов / Изменения статусов студентов' },
  { value: 'Онлайн-обучение', label: 'Онлайн-обучение' },
  { value: 'Цифровые системы', label: 'Цифровые системы' },
  { value: 'Обратная связь', label: 'Обратная связь' },
  { value: 'Дополнительное образование', label: 'Дополнительное образование' },
  { value: 'Безопасность', label: 'Безопасность' },
  { value: 'Наука', label: 'Наука' },
  { value: 'Социальные вопросы', label: 'Социальные вопросы' },
  { value: 'ВУЦ', label: 'ВУЦ' },
  { value: 'Общежития', label: 'Общежития' },
  { value: 'ОВЗ', label: 'ОВЗ' },
  { value: 'Внеучебка', label: 'Внеучебка' },
  { value: 'Выпускникам', label: 'Выпускникам' },
  { value: 'Другое', label: 'Другое' },
];


function App() {

  const [selectedCampus, setSelectedCampus] = useState('');
  const [selectedEducationLevel, setSelectedEducationLevel] = useState('');
  const [selectedQuestionCategory, setSelectedQuestionCategory] = useState('');

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
    return selectedOption ? selectedOption.label : '';
  };

  return (
    <div className="App">
      <h1>My App</h1>
      <MySelect
        label="Распределение по кампусам"
        options={campuses}
        value={selectedCampus}
        onChange={handleCampusChange}
      />
      <MySelect
        label="Разбивка по уровням образования"
        options={educationLevels}
        value={selectedEducationLevel}
        onChange={handleEducationLevelChange}
      />
      <MySelect
        label="Категории вопросов"
        options={questionCategories}
        value={selectedQuestionCategory}
        onChange={handleQuestionCategoryChange}
      />

      <p>Выбранный кампус: {getLabelByValue(selectedCampus, campuses)}</p>
      <p>Выбранный уровень образования: {getLabelByValue(selectedEducationLevel, educationLevels)}</p>
      <p>Выбранная категория вопросов: {getLabelByValue(selectedQuestionCategory, questionCategories)}</p>
      <div>
        {
          (() => {
            const filteredData = newMockData.filter(item => {
              let campusMatch = true;
              if (selectedCampus) {
                campusMatch = item.campus === selectedCampus;
              }
  
              let educationLevelMatch = true;
              if (selectedEducationLevel) {
                educationLevelMatch = item.education_level === selectedEducationLevel;
              }
  
              let questionCategoryMatch = true;
              if (selectedQuestionCategory) {
                questionCategoryMatch = item.question_category === selectedQuestionCategory;
              }
  
              return campusMatch && educationLevelMatch && questionCategoryMatch;
            });
  
            return JSON.stringify(filteredData);
          })()
        }
      </div>
    </div>
  );
}

export default App; 


