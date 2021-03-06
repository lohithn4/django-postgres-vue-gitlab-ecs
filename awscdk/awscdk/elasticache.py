import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_cloudformation as cloudformation,
    aws_elasticache as elasticache,
)


class ElastiCacheStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.elasticache_security_group = ec2.CfnSecurityGroup(
            self,
            "ElastiCacheSecurityGroup",
            vpc_id=scope.vpc.vpc_id,
            group_description="ElastiCacheSecurityGroup",
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    to_port=6379,
                    from_port=6379,
                    source_security_group_id=scope.vpc.vpc_default_security_group,
                )
            ],
        )

        self.elasticache_subnet_group = elasticache.CfnSubnetGroup(
            self,
            "CfnSubnetGroup",
            subnet_ids=scope.vpc.select_subnets(
                subnet_type=ec2.SubnetType.ISOLATED
            ).subnet_ids,
            description="The subnet group for ElastiCache",
        )

        self.elasticache = elasticache.CfnCacheCluster(
            self,
            "ElastiCacheClusterRedis",
            cache_node_type="cache.t2.micro",
            engine="redis",
            num_cache_nodes=1,
            vpc_security_group_ids=[
                self.elasticache_security_group.get_att("GroupId").to_string()
            ],
            cache_subnet_group_name=self.elasticache_subnet_group.ref,  # noqa
        )
