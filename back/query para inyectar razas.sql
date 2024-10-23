-- Inserta tipos de animales permitidos como mascotas en la tabla pet_types
INSERT INTO pet_types (type_name) VALUES 
('Perro'),
('Gato'),
('Ave'),
('Reptil'),
('Mamífero pequeño'),
('Pez'),
('Ave de corral'),
('Mamífero de corral');

-- Insertar razas y especies correspondientes en la tabla breeds

-- Razas de perros
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Labrador Retriever', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Pastor Alemán', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Bulldog Francés', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Golden Retriever', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Chihuahua', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Pomerania', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Beagle', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Dálmata', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Border Collie', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Shih Tzu', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Rottweiler', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Boxer', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Husky Siberiano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Dogo Argentino', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Bulldog Inglés', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro')),
('Doberman', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Perro'));

-- Razas de gatos
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Persa', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Siamés', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Maine Coon', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Bengalí', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Esfinge', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Ragdoll', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Abisinio', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Británico de Pelo Corto', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Devon Rex', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Chartreux', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Birmano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato')),
('Tonkinés', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Gato'));

-- Razas de aves
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Canario', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Periquito', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Cacatúa', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Loro Amazona', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Agapornis', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Papagayo Gris', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Ninfa', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Guacamayo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Cotorra Argentina', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Pinzón Cebra', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Periquito Australiano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave')),
('Paloma Mensajera', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave'));

-- Reptiles
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Iguana', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Gecko Leopardo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Pitón Bola', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Dragón Barbudo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Tortuga de Orejas Rojas', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Boa Constrictor', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Camaleón de Velo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Serpiente Rey de California', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil')),
('Tortuga Sulcata', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Reptil'));

-- Mamíferos pequeños
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Conejo Holandés', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Cuy Peruano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Hámster Sirio', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Rata Dumbo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Chinchilla', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Hurón', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Erizo Africano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Jerbo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño')),
('Conejo Enano', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero pequeño'));

-- Peces
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Pez Betta', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Guppy', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Pez Ángel', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Disco', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Pez Koi', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Neón', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Pez Globo', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Pez Payaso', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Tetra Cardenal', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez')),
('Goldfish', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Pez'));

-- Aves de corral
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Gallina Rhode Island Red', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Gallina Leghorn', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Pato Pekín', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Pato Muscovy', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Gallina Sussex', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Gallina Wyandotte', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral')),
('Gallina Plymouth Rock', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Ave de corral'));

-- Mamíferos de corral
INSERT INTO breeds (breed_name, pet_type_id) VALUES 
('Cabra Alpina', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Cabra Boer', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Vaca Jersey', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Oveja Merino', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Vaca Holstein', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Oveja Dorper', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral')),
('Caballo Árabe', (SELECT pet_type_id FROM pet_types WHERE type_name = 'Mamífero de corral'));
