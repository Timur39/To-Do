// Получаем элементы из HTML
const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');


// Массив для хранения задач (пока без сохранения в localStorage)
let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
let currentFilter = 'all'; // 'all', 'active', 'completed'

function renderTasks() {
    // Очищаем текущий список
    taskList.innerHTML = '';

    // Фильтруем задачи
    const filteredTasks = tasks.filter(task => {
        if (currentFilter === 'active') return !task.completed;
        if (currentFilter === 'completed') return task.completed;
        return true; // 'all'
    });

    // Для каждой задачи создаём элемент <li>
    tasks.forEach((task, index) => {
        taskList.innerHTML = '';
    
        const li = document.createElement('li');
        
        // Добавляем чекбокс для отметки выполнения
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = task.completed;
        
        // Добавляем обработчик изменения чекбокса
        checkbox.addEventListener('change', () => {
            tasks[index].completed = checkbox.checked;
            // Позже добавим сохранение в localStorage
        });

        // Добавляем класс для завершённых задач (для CSS)
        if (task.completed) {
            li.classList.add('completed');
        }

        // Добавляем текст задачи
        const text = document.createTextNode(task.text);

        // В цикле forEach после создания текста задачи:
        const textSpan = document.createElement('span');
        textSpan.textContent = task.text;

        // Заменяем текст на input при клике
        textSpan.addEventListener('click', () => {
            const editInput = document.createElement('input');
            editInput.type = 'text';
            editInput.value = task.text;

            // Заменяем span на input
            li.replaceChild(editInput, textSpan);
            editInput.focus();

            // Сохраняем изменения при нажатии Enter
            editInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    task.text = editInput.value.trim();
                    saveTasks();
                    renderTasks();
                }
            });
        });

        // Создаём кнопку удаления
        const deleteButton = document.createElement('button');
        deleteButton.textContent = '×'; // Символ "умножения" для кнопки
        deleteButton.addEventListener('click', () => {
            tasks.splice(index, 1); // Удаляем задачу из массива
            renderTasks(); // Перерисовываем список
        });

        // Собираем элемент
        li.appendChild(checkbox);
        li.appendChild(text);
        li.appendChild(deleteButton);
        
        // Добавляем элемент в список
        taskList.appendChild(li);

    });
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Обработчик отправки формы
taskForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Отменяем перезагрузку страницы
    
    if (taskInput.value.trim() === '') return; // Не добавляем пустые задачи

    // Добавляем задачу в массив
    tasks.push({
        text: taskInput.value,
        completed: false
    });

    saveTasks();


    // Очищаем поле ввода
    taskInput.value = '';

    // Обновляем список задач на экране
    renderTasks();
});





document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Убираем класс active у всех кнопок
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Добавляем класс active текущей кнопке
        button.classList.add('active');
        
        // Обновляем фильтр и перерисовываем задачи
        currentFilter = button.dataset.filter;
        renderTasks();
    });
});