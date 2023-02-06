class InfoMessage():
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """Печать результатов тренировки."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина одного шага.
    M_IN_KM: int = 1000  # Количество метров в одном километре.
    MINUTES: int = 60  # Количество минут в одном часе.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    M_IN_KM: int = 1000  # Количество метров в одном километре.
    MINUTES: int = 60  # Количество минут в одном часе.

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории
        для тренировки <Бег>."""

        duration_in_min = self.duration * self.MINUTES
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    KMH_IN_MSEC: float = 0.278  # Преобразование км/ч в м/с.
    HEIGHT_SM: int = 100  # Метр роста в сантиметрах.
    MINUTES: int = 60  # Количество минут в одном часе.

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории
        для тренировки <Спортивная ходьба>."""

        duration_in_min = self.duration * self.MINUTES
        meter_height = self.height / self.HEIGHT_SM
        m_sec_speed = (self.get_mean_speed()
                       * self.KMH_IN_MSEC)

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (m_sec_speed**2 / meter_height)
                * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
                * duration_in_min)


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2
    LEN_STEP: float = 1.38  # Длина одного гребка.
    M_IN_KM: int = 1000  # Количество метров в одном километре.

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Рассчитать среднюю скорость
        для тренировки <Плавание>."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Рассчитать потраченные калории
        для тренировки <Плавание>."""

        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""

    activity_dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type in activity_dict:
        return activity_dict[workout_type](*data)
    raise ValueError('Указан неверный код тренировки.')


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()  # Создание экземпляра InfoMessage.
    print(info.get_message())  # Вызов get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
