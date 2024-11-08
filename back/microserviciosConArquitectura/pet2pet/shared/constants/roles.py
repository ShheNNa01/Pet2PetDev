class RoleConstants:
    ADMIN = 1
    SUPER_ADMIN = 2

    @classmethod
    def is_valid_role(cls, role_id: int) -> bool:
        return role_id in [cls.ADMIN, cls.SUPER_ADMIN]