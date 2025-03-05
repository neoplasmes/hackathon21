import React, { useEffect, useMemo, useReducer, useState } from "react";
import { CheckboxGroup } from './components/CheckboxGroup'
import { filtersReducer, createInitialFiltersState } from "./model/reducer";
import { BarChart } from '@mui/x-charts/BarChart';
import "./App.css";
import { Stack } from "@mui/material";
import { calculateMean } from "./model/processors/calculateMean";

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

const serverURL = 'http://localhost:8000'


function App() {
  const [filtersState, dispatchFiltersChange] = useReducer(filtersReducer, new URLSearchParams(window.location.search), createInitialFiltersState);
  const [stats, setStats] = useState([]);

  useEffect(() => {
    console.log("useEffect")

    const getStats = async () => {
      const data = await fetch(serverURL + '/data', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json());

      setStats(data);
    }

    getStats();
  }, []);

  const meanStatsDistinguished = useMemo(() => {
    return Array.from(Object.entries(calculateMean(stats))).reduce((acc, [key, value]) => {
      if (key === 'response_time') {
        return acc;
      }

      acc.push({
        key,
        value,
      })

      return acc;
    }, []);
  }, [stats])

  console.log(meanStatsDistinguished)

  return (
      <div className="App">
        <Stack direction="row">
          <Stack direction="column">
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
          </Stack>
          <div>
            {stats.length > 0 && <BarChart
              dataset={meanStatsDistinguished}
              xAxis={[{ scaleType: 'band', dataKey: 'key', valueFormatter: (v, ctx) => ctx.location === "tick" ? v.substring(0, 3) + '...' : v }]}
              series={[{ dataKey: 'value' }]}
              width={750}
              height={300}
            />}
          </div>
        </Stack>
      </div>
    );
}

export default App;
