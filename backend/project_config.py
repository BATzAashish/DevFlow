class ProjectConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProjectConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.project_path = ""
        self.project_name = ""
        self.project_description = ""
        self.tech_stack = ""
        
    @property
    def is_tech_stack_set(self):
        return bool(self.tech_stack.strip())
    
    def update_project_info(self, path="", name="", description=""):
        if path:
            self.project_path = path
        if name:
            self.project_name = name
        if description:
            self.project_description = description
            
    def update_tech_stack(self, tech_stack):
        self.tech_stack = tech_stack
        
    def get_project_info(self):
        return {
            "path": self.project_path,
            "name": self.project_name,
            "description": self.project_description,
            "tech_stack": self.tech_stack
        }
