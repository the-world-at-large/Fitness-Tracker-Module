class InfoMessage():
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистания: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f}  км/ч; '
                f'Потрачено ккал: {self.calories:.3f}')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Длина одного шага.
    M_IN_KM = 1000  # Количество метров в одном километре.
    MINUTES: int = 60  # Количество минут в одном часе.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    M_IN_KM = 1000  # Количество метров в одном километре.
    MINUTES: int = 60  # Количество минут в одном часе.

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULPTIPLIER = 0.035
    CALORIES_WEIGHT_MULPTIPLIER_2 = 0.029
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.278
    HEIGHT_SM = 100  # Метр роста в сантиметрах.
    MINUTES: int = 60  # Количество минут в одном часе.

    def __init__(self, action: int, duration: float,
                 weight: float, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории."""
        return (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed()
                    * self.CALORIES_MEAN_SPEED_MULTIPLIER) ** 2
                    / (self.height / self.HEIGHT_SM)
                    * self.CALORIES_WEIGHT_MULPTIPLIER_2
                    * self.weight) * (self.duration * self.MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_MULTIPLER = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2
    HEIGHT_SM = 100  # Количество сантиметров в одном метре роста.
    LEN_STEP = 1.38  # Длина одного гребка.
    M_IN_KM = 1000  # Количество метров в одном километре.

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчитать среднюю скорость."""
        return ((self.length_pool / self.HEIGHT_SM)
                * (self.count_pool / self.M_IN_KM) / self.duration)

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLER)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    final = info.get_message()
    print(final)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
