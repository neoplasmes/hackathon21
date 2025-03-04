const educationLevels = new Map(Object.entries({
    bak: 'Бакалавриат',
    mag: 'Магистратура',
    spec: 'Специалитет',
    asp: 'Аспирантура'
}));

const campuses = new Map(Object.entries({
    msc: "Москва",
    nn: "Нижний Новгород",
    spb: "Санкт-Петербург",
    prm: "Пермь"
}));

const questionCategories = new Map(Object.entries({
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

const abbreviationsToRussian = {
    [abbreviations.campuses]: 'Кампус',
    [abbreviations.educactionLevels]: 'Уровень образования',
    [abbreviations.questionCategories]: 'Категории вопросов'
};

export {
    abbreviationsToRussian,
    abbreviations,
    campuses,
    questionCategories,
    educationLevels
};