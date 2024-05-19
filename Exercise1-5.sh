# Создаем файлы и заполняем их данными
cat > "Домашние животные" << EOF
Собаки
Кошки
Хомяки
EOF

cat > "Вьючные животные" << EOF
Лошади
Верблюды
Ослы
EOF

# Объединяем файлы в один
cat "Домашние животные" "Вьючные животные" > "Друзья человека"

# Просмотр содержимого созданного файла
cat "Друзья человека"

# Переименовываем файл
mv "Друзья человека" "Friends_of_Human"

# Создаем директорию
mkdir MyDirectory

# Перемещаем файл в эту директорию
mv "Friends_of_Human" /home/vboxuser/MyDirectory


#Меняем пользователя на root
su root

#Обновляем и устанавливаем пакет mysql
apt update
apt install mysql-server

#Устанавливаем дополнительный пакет mysql
apt install mysql-client

#Меняем директорию
cd /home/vboxuser/Downloads

#Устанавливаем и удаляем скаченный deb пакет
dpkg -i gimp_2.10.18-1ubuntu0.1_amd64.deb
dpkg -r gimp

# Просмотр истории команд
history