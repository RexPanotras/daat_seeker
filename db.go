package database

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

var DB *sql.DB

// 内容结构体
type Content struct {
	ID          int    `json:"id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Interface   string `json:"interface"`
	Subject     string `json:"subject"`
	Tags        string `json:"tags"`
	Type        string `json:"type"`
}

// 标签结构体
type Tag struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Color string `json:"color"`
}

// 初始化数据库
func InitDB() {
	var err error
	DB, err = sql.Open("sqlite3", "./database/questions.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}

	// 创建表
	err = createTables()
	if err != nil {
		log.Fatalf("Failed to create tables: %v", err)
	}

	// 插入初始数据
	err = insertInitialData()
	if err != nil {
		log.Fatalf("Failed to insert initial data: %v", err)
	}

	fmt.Println("Database initialized successfully")
}

// 创建表
func createTables() error {
	// 创建内容表
	_, err := DB.Exec(`
	CREATE TABLE IF NOT EXISTS contents (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		description TEXT NOT NULL,
		interface TEXT NOT NULL,
		subject TEXT NOT NULL,
		tags TEXT NOT NULL,
		type TEXT NOT NULL DEFAULT 'question'
	)
	`)
	if err != nil {
		return err
	}

	// 创建标签表
	_, err = DB.Exec(`
	CREATE TABLE IF NOT EXISTS tags (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		color TEXT NOT NULL
	)
	`)
	if err != nil {
		return err
	}

	return nil
}

// 插入初始数据
func insertInitialData() error {
	// 检查标签表是否为空
	var count int
	err := DB.QueryRow("SELECT COUNT(*) FROM tags").Scan(&count)
	if err != nil {
		return err
	}

	// 如果标签表为空，插入初始标签
	if count == 0 {
		_, err = DB.Exec(`
		INSERT INTO tags (name, color) VALUES
		('数学', '#4CAF50'),
		('物理学', '#2196F3'),
		('计算机科学', '#FF9800'),
		('调和级数', '#9C27B0'),
		('洛伦兹变换', '#F44336')
		`)
		if err != nil {
			return err
		}
	}

	// 检查内容表是否为空
	err = DB.QueryRow("SELECT COUNT(*) FROM contents").Scan(&count)
	if err != nil {
		return err
	}

	// 如果内容表为空，插入初始内容
	if count == 0 {
		_, err = DB.Exec(`
		INSERT INTO contents (title, description, interface, subject, tags, type) VALUES
		('调和级数求和', '调和级数是发散的。虽然其增长速度非常缓慢（近似于ln(n)+γ，其中γ≈0.5772是欧拉-马歇罗尼常数），但随着n增大，其和会无限增大。这是数学分析中的经典结论，由中世纪数学家尼克尔·奥雷姆（Nicole Oresme）首次证明。', '/api/calculate/harmonic', '数学', '数学,调和级数', 'question'),
		('寻找调和级数项数', '给定目标值，找到最小的n使得调和级数Hn大于等于目标值。调和级数H_n = 1 + 1/2 + 1/3 + ... + 1/n，随着n的增加，H_n会无限增大，但增长非常缓慢。', '/api/calculate/harmonic/inverse', '数学', '数学,调和级数', 'question'),
		('洛伦兹变换', '洛伦兹变换是狭义相对论的核心，描述了两个惯性参考系之间的时空坐标转换。它基于两个基本假设：相对性原理和光速不变原理。洛伦兹变换已被无数实验验证，包括粒子加速器中的时间膨胀效应、GPS卫星的时间校正等。', '/api/calculate/lorentz', '物理学', '物理学,洛伦兹变换', 'question')
		`)
		if err != nil {
			return err
		}
	}

	return nil
}

// 获取所有内容
func GetAllContents() ([]Content, error) {
	rows, err := DB.Query("SELECT id, title, description, interface, subject, tags, type FROM contents")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var contents []Content
	for rows.Next() {
		var c Content
		err := rows.Scan(&c.ID, &c.Title, &c.Description, &c.Interface, &c.Subject, &c.Tags, &c.Type)
		if err != nil {
			return nil, err
		}
		contents = append(contents, c)
	}

	return contents, nil
}

// 根据ID获取内容
func GetContentByID(id int) (Content, error) {
	var c Content
	err := DB.QueryRow("SELECT id, title, description, interface, subject, tags, type FROM contents WHERE id = ?", id).Scan(
		&c.ID, &c.Title, &c.Description, &c.Interface, &c.Subject, &c.Tags, &c.Type,
	)
	if err != nil {
		return Content{}, err
	}

	return c, nil
}

// 获取所有学科
func GetAllSubjects() ([]string, error) {
	rows, err := DB.Query("SELECT DISTINCT subject FROM contents")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var subjects []string
	for rows.Next() {
		var subject string
		err := rows.Scan(&subject)
		if err != nil {
			return nil, err
		}
		subjects = append(subjects, subject)
	}

	return subjects, nil
}

// 根据学科获取内容
func GetContentsBySubject(subject string) ([]Content, error) {
	rows, err := DB.Query("SELECT id, title, description, interface, subject, tags, type FROM contents WHERE subject = ?", subject)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var contents []Content
	for rows.Next() {
		var c Content
		err := rows.Scan(&c.ID, &c.Title, &c.Description, &c.Interface, &c.Subject, &c.Tags, &c.Type)
		if err != nil {
			return nil, err
		}
		contents = append(contents, c)
	}

	return contents, nil
}

// 获取所有标签
func GetAllTags() ([]Tag, error) {
	rows, err := DB.Query("SELECT id, name, color FROM tags")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tags []Tag
	for rows.Next() {
		var t Tag
		err := rows.Scan(&t.ID, &t.Name, &t.Color)
		if err != nil {
			return nil, err
		}
		tags = append(tags, t)
	}

	return tags, nil
}
