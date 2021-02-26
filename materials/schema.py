import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required

from .models import Material, Trashcan, Product, UserProduct


class MaterialList(DjangoObjectType):
    class Meta:
        model = Material
        fields = ("id", "name", "decay")


class TrashcanList(DjangoObjectType):
    class Meta:
        model = Trashcan
        fields = ("id", "material", "latitude", "longitude")


class ProductList(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("material", "code", "name", "id")


class UserProductList(DjangoObjectType):
    class Meta:
        model = UserProduct
        fields = ("user", "product", "added", "id")


class AddRecyclingLocation(graphene.Mutation):
    material = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        material = graphene.String(required=True)
        latitude = graphene.String(required=True)
        longitude = graphene.String(required=True)

    @login_required
    @superuser_required
    def mutate(self, info, material, latitude, longitude):
        newLocation = Trashcan(
            material=material, latitude=latitude, longitude=longitude)
        newLocation.save()
        return AddRecyclingLocation(material=material, latitude=latitude, longitude=longitude, success=True)


class AddMaterial(graphene.Mutation):
    name = graphene.String()
    decay = graphene.Int()
    success = graphene.Boolean()

    class Arguments:
        name = graphene.String(required=True)
        decay = graphene.Int(required=True)

    @login_required
    @superuser_required
    def mutate(self, info, name, decay):
        newMaterial = Material(name=name, decay=decay)
        newMaterial.save()
        return AddMaterial(name=name, decay=decay, success=True)


class AddProduct(graphene.Mutation):
    material_name = graphene.String()
    code = graphene.String()
    name = graphene.String()
    success = graphene.Boolean()
    error = graphene.String(required=False)

    class Arguments:
        material_name = graphene.String()
        code = graphene.String(required=False)
        name = graphene.String()

    def mutate(self, info, name, **kwargs):
        code = kwargs.get("code", 0)
        material_name = kwargs.get("material_name", None)
        if(material_name != None):
            try:
                currentMaterial = Material.objects.get(name=material_name)
            except Material.DoesNotExist:
                return AddProduct(material_name, code, name, False)

            try:
                productFromName = Product.objects.get(name=name)
            except Product.DoesNotExist:
                newProduct = Product(material=Material.objects.get(
                    name=material_name), code=code, name=name)
                newProduct.save()
                return AddProduct(material_name, code, name, True)
            return AddProduct(material_name, code, name, False, "Already Exists")
        return AddProduct(material_name, code, name, False)


class AddRecycledItem(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        product_name = graphene.String()
        code = graphene.String()

    def mutate(self, info, **kwargs):
        product_name = kwargs.get("product_name", None)
        code = kwargs.get("code", None)
        if(code != None):
            try:
                currentProduct = Product.objects.get(code=code)
            except Product.DoesNotExist:
                return AddRecycledItem(False)
            newUserProduct = UserProduct(
                user=info.context.user.profile, product=currentProduct)
            newUserProduct.save()
            info.context.user.profile.recycled += 1
            info.context.user.profile.years_saved += currentProduct.material.decay
            info.context.user.profile.save()
            return AddRecycledItem(True)

        elif(product_name != None):
            try:
                currentProduct = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return AddRecycledItem(False)
            newUserProduct = UserProduct(
                user=info.context.user.profile, product=currentProduct)
            newUserProduct.save()
            info.context.user.profile.recycled += 1
            info.context.user.profile.years_saved += currentProduct.material.decay
            return AddRecycledItem(True)
        return AddRecycledItem(False)


class Query(graphene.ObjectType):

    all_materials = graphene.List(
        MaterialList, name=graphene.String(required=False))

    recycling_locations = graphene.List(
        TrashcanList, material=graphene.String(required=False))

    item_products = graphene.List(
        ProductList, code=graphene.String(required=False)
    )
    item_products_by_material = graphene.List(
        ProductList, material=graphene.String(required=True))

    def resolve_all_materials(self, info, **kwargs):
        material = kwargs.get("name")
        if material == None:
            return Material.objects.all()
        else:
            try:
                materials = Material.objects.filter(name=material)
            except Material.DoesNotExist:
                return None
            return materials

    def resolve_item_products(self, info, **kwargs):
        code = kwargs.get("code")
        if code == None:
            return Product.objects.all()
        else:
            try:
                product = Product.objects.filter(code=code)
            except Product.DoesNotExist:
                return None
            return product

    def resolve_item_products_by_material(self, info, **kwargs):
        material = kwargs.get("material")
        if material == None:
            return Product.objects.all()
        else:
            try:
                material = Material.objects.get(name=material)
            except Material.DoesNotExist:
                return None
            try:
                products = Product.objects.filter(material=material)
            except Product.DoesNotExist:
                return None
            return products

    def resolve_recycling_locations(self, info, **kwargs):
        material = kwargs.get("material")
        if material == None:
            return Trashcan.objects.all()
        else:
            try:
                locations = Trashcan.objects.filter(material=material)
            except Trashcan.DoesNotExist:
                return None
            return locations


class Mutation(graphene.ObjectType):
    add_recycling_location = AddRecyclingLocation.Field()
    add_material = AddMaterial.Field()
    add_product = AddProduct.Field()
    add_recycled_item = AddRecycledItem.Field()


schema = graphene.Schema(query=Query)
