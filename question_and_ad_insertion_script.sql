INSERT INTO questions (question, options, correct_index, question_type, category, ad_id)
VALUES
-- 1
('Which Mauryan emperor renounced violence and converted to Buddhism after the Kalinga War?',
 ARRAY['Samudragupta', 'Ashoka', 'Chandragupta Maurya', 'Bindusara'], 
 1, 'MCQ', 'history', NULL),

-- 2
('The Nalanda University was destroyed by which invader in the 12th century?',
 ARRAY['Bakhtiyar Khilji', 'Muhammad Ghori', 'Mahmud of Ghazni', 'Alauddin Khilji'],
 0, 'MCQ', 'history', NULL),

-- 3
('Who was the founder of the Chola Dynasty that led its imperial expansion?',
 ARRAY['Rajaraja Chola II', 'Kulothunga Chola I', 'Rajaraja Chola I', 'Vijayalaya Chola'],
 3, 'MCQ', 'history', NULL),

-- 4
('The Treaty of Purandar was signed between Shivaji and which Mughal general?',
 ARRAY['Raja Jai Singh I', 'Shaista Khan', 'Mir Jumla', 'Aurangzeb'],
 0, 'MCQ', 'history', NULL),

-- 5
('The Battle of Buxar (1764) was fought between the British East India Company and whom?',
 ARRAY['Shah Alam II & allies', 'Tipu Sultan', 'Marathas', 'Siraj ud-Daulah'],
 0, 'MCQ', 'history', NULL),

-- 6
('Who was the Viceroy of India during the Partition of Bengal in 1905?',
 ARRAY['Lord Curzon', 'Lord Ripon', 'Lord Minto', 'Lord Canning'],
 0, 'MCQ', 'history', NULL),

-- 7
('Which movement marked the beginning of organized nationalist activity in India?',
 ARRAY['Quit India Movement', 'Civil Disobedience Movement', 'Swadeshi Movement', 'Non-Cooperation Movement'],
 2, 'MCQ', 'history', NULL),

-- 8
('The term "Drain of Wealth" was first used by which nationalist leader?',
 ARRAY['Bal Gangadhar Tilak', 'Dadabhai Naoroji', 'Lala Lajpat Rai', 'Gopal Krishna Gokhale'],
 1, 'MCQ', 'history', NULL),

-- 9
('Which Indian revolutionary founded the Hindustan Socialist Republican Association (HSRA)?',
 ARRAY['Bhagat Singh', 'Ram Prasad Bismil', 'Chandrashekhar Azad', 'Sukhdev'],
 1, 'MCQ', 'history', NULL),

-- 10
('Who presided over the Lahore Session of the Indian National Congress in 1929?',
 ARRAY['Jawaharlal Nehru', 'Rajendra Prasad', 'Sardar Patel', 'Mahatma Gandhi'],
 0, 'MCQ', 'history', NULL),

-- 11
('Who was the first Indian woman President of the Indian National Congress?',
 ARRAY['Annie Besant', 'Vijaya Lakshmi Pandit', 'Sarojini Naidu', 'Aruna Asaf Ali'],
 0, 'MCQ', 'history', NULL),

-- 12
('The Cabinet Mission Plan came to India in which year?',
 ARRAY['1946', '1947', '1945', '1942'],
 0, 'MCQ', 'history', NULL),

-- 13
('Who was the commander of the British forces during the Battle of Plassey in 1757?',
 ARRAY['Robert Clive', 'Lord Wellesley', 'Warren Hastings', 'Lord Cornwallis'],
 0, 'MCQ', 'history', NULL),

-- 14
('The Home Rule League in India was launched by Bal Gangadhar Tilak and whom?',
 ARRAY['Annie Besant', 'Lala Lajpat Rai', 'Gopal Krishna Gokhale', 'Bipin Chandra Pal'],
 0, 'MCQ', 'history', NULL),

-- 15
('Which leader gave the slogan “Do or Die” during the Quit India Movement?',
 ARRAY['Jawaharlal Nehru', 'Sardar Patel', 'Subhas Chandra Bose', 'Mahatma Gandhi'],
 3, 'MCQ', 'history', NULL);


-- Insert ad content
INSERT INTO ads (title, content, duration)
VALUES (
  'Incredible India Tourism Campaign',
  'Incredible India is a campaign by the Government of India to promote tourism and highlight the cultural richness and historical diversity of India. It showcases destinations, heritage sites, and unique experiences like Ayurveda, Yoga, and rural tourism.',
  15
);