from dao.organization import OrganizationDAO

from model.organization import OrganizationCreate, OrganizationUpdate, OrganizationBase

from typing import List

class Organization:
    @staticmethod
    async def create_organization(organization_data: OrganizationCreate) -> OrganizationBase:
        new_organization_data = await OrganizationDAO.insert(organization_data)
        return new_organization_data

    @staticmethod
    async def get_organization(organizationid: int) -> OrganizationBase:
        organization_data = await OrganizationDAO.get(organizationid)
        return organization_data
    
    @staticmethod
    async def get_all_organizations() -> List[OrganizationBase]:
        organization_data = await OrganizationDAO.get_all()
        return organization_data

    @staticmethod
    async def update_organization(organizationid: int, organization_data: OrganizationUpdate) -> OrganizationBase:
        updated_organization_data = await OrganizationDAO.update(organizationid, organization_data)
        return updated_organization_data

    @staticmethod
    async def delete_organization(organizationid: int) -> bool:
        return await OrganizationDAO.delete(organizationid)
