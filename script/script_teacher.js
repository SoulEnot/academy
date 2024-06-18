addEventListener("DOMContentLoaded", (event) => {
    event.preventDefault();

    fetch('/teacher')
    .then(response => response.json())
    .then(data => {
        // data.forEach(data => {
            const teacherName = data.name;
            const teacherSurname = data.surname;
            const teacherPosition = data.position;
            const teacherSalary = data.salary;
            const teacherPremium = data.premium;

            const name = document.getElementById('teacher-name');
            name.textContent = teacherName + ' ' + teacherSurname;

            const position = document.getElementById('teacher-position');
            position.textContent = teacherPosition;

            const salary = document.getElementById('teacher-salary');
            salary.textContent = teacherSalary + ' Руб.';

            const premium = document.getElementById('teacher-premium');
            premium.textContent = teacherPremium + ' Руб.';
        // });
    })
    .catch(error => console.error('Error: ', error));
});