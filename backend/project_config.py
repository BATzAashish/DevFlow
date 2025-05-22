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
        self.has_venv = False
        self.has_git = False
        self.file_structure = ""
        self.implementation = ""
        self.testing_strategy = ""
        self.deployment_strategy = ""
        self.readme = ""
        
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
        
    def update_project_path(self, path):
        self.project_path = path
        
    def set_venv_status(self, status):
        self.has_venv = status
        
    def set_git_status(self, status):
        self.has_git = status

    def update_file_structure(self, structure):
        self.file_structure = structure
    
    def update_implementation(self, implementation):
        self.implementation = implementation

    def update_testing_strategy(self, strategy):
        self.testing_strategy = strategy
        
    def update_deployment_strategy(self, strategy):
        self.deployment_strategy = strategy
        
    def update_readme(self, readme):
        self.readme = readme
        
    def get_project_info(self):
        return {
            "path": self.project_path,
            "name": self.project_name,
            "description": self.project_description,
            "tech_stack": self.tech_stack,
            "file_structure": self.file_structure,
            "has_venv": self.has_venv,
            "has_git": self.has_git,
            "implementation": self.implementation,
            "testing_strategy": self.testing_strategy,
            "deployment_strategy": self.deployment_strategy,
            "readme": self.readme
        }
