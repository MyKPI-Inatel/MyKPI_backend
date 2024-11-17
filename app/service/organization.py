from dao.organization import OrganizationDAO

from model.organization import OrganizationCreate, OrganizationUpdate, OrganizationBase

from typing import List

class Organization:
    @staticmethod
    async def create_organization(organization_data: OrganizationCreate) -> OrganizationBase:
        return await OrganizationDAO.insert(organization_data)

    @staticmethod
    async def get_organization(organizationid: int) -> OrganizationBase:
        return await OrganizationDAO.get(organizationid)
    
    @staticmethod
    async def get_all_organizations() -> List[OrganizationBase]:
        return await OrganizationDAO.get_all()

    @staticmethod
    async def update_organization(organizationid: int, organization_data: OrganizationUpdate) -> OrganizationBase:
        return await OrganizationDAO.update(organizationid, organization_data)

    @staticmethod
    async def delete_organization(organizationid: int) -> bool:
        return await OrganizationDAO.delete(organizationid)
